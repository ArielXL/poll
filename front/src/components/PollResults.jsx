function PollResults({ results }) {
  if (!results) {
    return (
      <section className="card">
        <h2>Resultados</h2>
        <p>Selecciona una encuesta para ver sus resultados.</p>
      </section>
    );
  }

  const choices = Array.isArray(results.choices) ? results.choices : [];
  const totalVotes = Number(results.total_votes ?? 0);

  return (
    <section className="card">
      <h2>Resultados</h2>

      <h3>{results.question}</h3>
      <p>Total de votos: {totalVotes}</p>

      {choices.length === 0 ? (
        <p>Esta encuesta todavía no tiene opciones o resultados disponibles.</p>
      ) : (
        choices.map((choice, index) => {
          const votes = Number(choice.votes ?? choice.votes_count ?? 0);

          const percentage =
            totalVotes > 0 ? ((votes / totalVotes) * 100).toFixed(1) : 0;

          return (
            <div className="result-item" key={index}>
              <div className="result-header">
                <span>{choice.text}</span>
                <span>
                  {votes} votos - {percentage}%
                </span>
              </div>

              <div className="bar">
                <div
                  className="bar-fill"
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
            </div>
          );
        })
      )}
    </section>
  );
}

export default PollResults;