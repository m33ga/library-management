const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/";


interface Credentials {
  email: string;
  password: string;
}

interface User {
  username: string;
  email: string;
  password: string;
  selectedInstitution: number;
}


export const login = async (credentials: Credentials) => {
  try {
    const response = await fetch(`${API_URL}login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      throw new Error("Login error. Check your credentials.");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error when logging in:", error);
    throw error;
  }
};

export const register = async (user: User) => {
  try {
    const response = await fetch(`${API_URL}signup/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    });

    if (!response.ok) {
      throw new Error("Registration error. Check your data.");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error when registering:", error);
    throw error;
  }
}