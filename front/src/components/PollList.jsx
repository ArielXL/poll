import { useState } from "react";
import { vote } from "../api/questionnaireApi";

function PollList({ polls = [], onVote, onShowResults }) {
  const [loadingChoiceId, setLoadingChoiceId] = useState(null);
  const [message, setMessage] = useState("");
  const [userIdentifier, setUserIdentifier] = useState("");

  const safePolls = Array.isArray(polls) ? polls : [];

  const handleVote = async (choiceId) => {
    if (!userIdentifier.trim()) {
      setMessage("Debes escribir quién está votando.");
      return;
    }

    try {
      setMessage("");
      setLoadingChoiceId(choiceId);

      await vote(choiceId, userIdentifier.trim());

      setMessage("Voto registrado correctamente.");
      onVote();
    } catch (error) {
      setMessage("No se pudo registrar el voto.");
    } finally {
      setLoadingChoiceId(null);
    }
  };

  return (
    <section className="card">
      <h2>Encuestas disponibles</h2>

      <div className="voter-box">
        <label>Nombre o identificador del votante</label>
        <input
          type="text"
          placeholder="Ej: ariel, usuario1, correo@dominio.com"
          value={userIdentifier}
          onChange={(e) => setUserIdentifier(e.target.value)}
        />
      </div>

      {message && <p className="message">{message}</p>}

      {safePolls.length === 0 ? (
        <div className="empty">
          <h3>No hay encuestas todavía</h3>
          <p>Crea la primera encuesta para comenzar.</p>
        </div>
      ) : (
        safePolls.map((poll) => (
          <div className="poll-item" key={poll.id}>
            <h3>{poll.question}</h3>

            <div className="choices-container">
              {poll.choices?.map((choice) => (
                <button
                  key={choice.id}
                  onClick={() => handleVote(choice.id)}
                  disabled={loadingChoiceId === choice.id}
                >
                  {loadingChoiceId === choice.id ? "Votando..." : choice.text}
                </button>
              ))}
            </div>

            <button
              className="secondary"
              onClick={() => onShowResults(poll.id)}
            >
              Ver resultados
            </button>
          </div>
        ))
      )}
    </section>
  );
}

export default PollList;