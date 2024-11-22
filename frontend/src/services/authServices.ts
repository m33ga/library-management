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

interface Institution {
  id: number;
  name: string;
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
    localStorage.setItem("authToken", data.token);
    return { success: true, data };
  } catch (error) {
    console.error("Error when logging in:", error);
    throw error;
  }
};

export const register = async (user: User) => {
  try {
    const payload = {
      username: user.username,
      email: user.email,
      password: user.password,
      institution_id: user.institution,
    };

    const response = await fetch(`${API_URL}signup/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      const errorMessage =
        errorData.email?.[0] || errorData.username?.[0] || "Invalid input.";
      console.error("Error when registering:", errorData);
      return { success: false, error: errorMessage };
    }

    const data = await response.json();
    localStorage.setItem("authToken", data.token);
    return { success: true, data };
  } catch (error) {
    console.error("Error when registering:", error);
    throw error;
  }
};

export const getInstitutions = async (): Promise<{
  success: boolean;
  data?: Institution[];
  error?: any;
}> => {
  try {
    const response = await fetch(`${API_URL}list_institutions/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error when fetching institutions:", errorData);
      return { success: false, error: errorData };
    }

    const data: Institution[] = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error("Error when fetching institutions:", error);
    return { success: false, error };
  }
};
