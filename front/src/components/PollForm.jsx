import { useState } from "react";
import { createPoll } from "../api/questionnaireApi";

function PollForm({ onPollCreated }) {
  const [question, setQuestion] = useState("");
  const [choices, setChoices] = useState(["", ""]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChoiceChange = (index, value) => {
    const updatedChoices = [...choices];
    updatedChoices[index] = value;
    setChoices(updatedChoices);
  };

  const addChoice = () => {
    setChoices([...choices, ""]);
  };

  const removeChoice = (index) => {
    if (choices.length <= 2) return;
    setChoices(choices.filter((_, i) => i !== index));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    const cleanChoices = choices
      .map((choice) => choice.trim())
      .filter((choice) => choice !== "");

    if (!question.trim()) {
      setError("La pregunta es obligatoria.");
      return;
    }

    if (cleanChoices.length < 2) {
      setError("Debes agregar al menos 2 opciones.");
      return;
    }

    try {
      setLoading(true);

      await createPoll({
        question: question.trim(),
        choices: cleanChoices,
      });

      setQuestion("");
      setChoices(["", ""]);
      onPollCreated();
    } catch (error) {
      setError("No se pudo crear la encuesta.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Crear encuesta</h2>

      <form onSubmit={handleSubmit}>
        <label>Pregunta</label>
        <input
          type="text"
          placeholder="Ej: ¿Lenguaje favorito?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <label>Opciones</label>

        {choices.map((choice, index) => (
          <div className="choice-row" key={index}>
            <input
              type="text"
              placeholder={`Opción ${index + 1}`}
              value={choice}
              onChange={(e) => handleChoiceChange(index, e.target.value)}
            />

            <button
              type="button"
              className="secondary"
              onClick={() => removeChoice(index)}
              disabled={choices.length <= 2}
            >
              Quitar
            </button>
          </div>
        ))}

        <button type="button" className="secondary" onClick={addChoice}>
          Agregar opción
        </button>

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Creando..." : "Crear encuesta"}
        </button>
      </form>
    </section>
  );
}

export default PollForm;