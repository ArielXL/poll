import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/questionnaire",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getPolls = async () => {
  const response = await api.get("/polls/");
  return response.data;
};

export const createPoll = async (pollData) => {
  const response = await api.post("/polls/", pollData);
  return response.data;
};

export const vote = async (choiceId, userIdentifier) => {
  const response = await api.post("/vote/", {
    choice_id: choiceId,
    user_identifier: userIdentifier,
  });

  return response.data;
};

export const getPollResults = async (pollId) => {
  const response = await api.get(`/polls/${pollId}/results/`);
  return response.data;
};