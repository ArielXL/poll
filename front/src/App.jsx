import { useEffect, useState } from "react";
import { getPolls, getPollResults } from "./api/questionnaireApi";
import PollForm from "./components/PollForm";
import PollList from "./components/PollList";
import PollResults from "./components/PollResults";

function App() {
  const [polls, setPolls] = useState([]);
  const [selectedResults, setSelectedResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadPolls = async () => {
    try {
      setError("");
      const data = await getPolls();

      if (Array.isArray(data)) {
        setPolls(data);
      } else if (Array.isArray(data.results)) {
        setPolls(data.results);
      } else {
        setPolls([]);
      }
    } catch (error) {
      setError("No se pudieron cargar las encuestas.");
    } finally {
      setLoading(false);
    }
  };

  const handleShowResults = async (pollId) => {
    try {
      setError("");
      const data = await getPollResults(pollId);
      setSelectedResults(data);
    } catch (error) {
      setError("No se pudieron cargar los resultados.");
    }
  };

  useEffect(() => {
    loadPolls();
  }, []);

  return (
    <main className="container">
      {error && <p className="error">{error}</p>}

      <PollForm onPollCreated={loadPolls} />

      {loading ? (
        <div className="loader-container">
          <div className="spinner"></div>
          <p>Cargando encuestas...</p>
        </div>
      ) : (
        <div className="grid">
          <PollList
            polls={polls}
            onVote={loadPolls}
            onShowResults={handleShowResults}
          />

          <PollResults results={selectedResults} />
        </div>
      )}
    </main>
  );
}

export default App;