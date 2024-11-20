const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/";


interface Credentials {
  email: string;
  password: string;
}

interface User {
  username: string;
  email: string;
  password: string;
  institution: number;
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
      const errorData = await response.json();
      console.error("Error when logging in:", errorData);
      return { success: false, error: errorData };
    }

    const data = await response.json();
    return { success: true, data };
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
      const errorData = await response.json();
      const errorMessage = errorData.email ? errorData.email[0] : errorData.username[0];
      console.log("Error when registering:", errorMessage);
      return { success: false, error: errorMessage };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    let errorMessage = "Erro desconhecido";
    if (error instanceof Error) {
      errorMessage = error.message;
    }
    console.log("Error when registering:", errorMessage);
    throw new Error(errorMessage);
  }
}