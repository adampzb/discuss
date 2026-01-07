import api from "./api";
import {
  loginSuccess,
  loginFailure,
  registerSuccess,
  logout as logoutAction,
} from "../features/auth/authSlice";
import type { AppDispatch } from "../store";

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterCredentials {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export const login =
  (credentials: LoginCredentials) => async (dispatch: AppDispatch) => {
    try {
      const response = await api.post("/users/login/", credentials);

      const { user, access, refresh } = response.data;

      // Store tokens and user data
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
      localStorage.setItem("user", JSON.stringify(user));

      dispatch(
        loginSuccess({ user, accessToken: access, refreshToken: refresh }),
      );

      return { success: true };
    } catch (error) {
      const axiosError = error as { response?: { data?: { detail?: string } } };
      const errorMessage =
        axiosError.response?.data?.detail ||
        (error as Error).message ||
        "Login failed";
      dispatch(loginFailure(errorMessage));
      return { success: false, error: errorMessage };
    }
  };

export const register =
  (userData: RegisterCredentials) => async (dispatch: AppDispatch) => {
    try {
      const response = await api.post("/users/register/", userData);

      const { user, access, refresh } = response.data;

      // Store tokens and user data
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
      localStorage.setItem("user", JSON.stringify(user));

      dispatch(
        registerSuccess({ user, accessToken: access, refreshToken: refresh }),
      );

      return { success: true };
    } catch (error) {
      const axiosError = error as { response?: { data?: { detail?: string } } };
      const errorMessage =
        axiosError.response?.data?.detail ||
        (error as Error).message ||
        "Registration failed";
      dispatch(loginFailure(errorMessage));
      return { success: false, error: errorMessage };
    }
  };

export const logout = () => async (dispatch: AppDispatch) => {
  try {
    const refreshToken = localStorage.getItem("refreshToken");
    if (refreshToken) {
      await api.post("/users/logout/", { refresh: refreshToken });
    }
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    // Clear local storage
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");

    // Dispatch logout action
    dispatch(logoutAction());
  }
};

export const checkAuth = () => (dispatch: AppDispatch) => {
  const accessToken = localStorage.getItem("accessToken");
  const refreshToken = localStorage.getItem("refreshToken");
  const userData = localStorage.getItem("user");

  if (accessToken && refreshToken && userData) {
    const user = JSON.parse(userData);
    dispatch(
      loginSuccess({
        user,
        accessToken,
        refreshToken,
      }),
    );
  }
};
