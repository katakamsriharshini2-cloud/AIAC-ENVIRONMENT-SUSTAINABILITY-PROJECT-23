import React, { createContext, useContext, useState, useEffect } from "react";
import { authApi } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("ecosphere_token");
    if (token) {
      authApi.me()
        .then(setUser)
        .catch(() => localStorage.removeItem("ecosphere_token"))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (emailOrToken, passwordOrUser) => {
    if (typeof passwordOrUser === "object" && passwordOrUser !== null) {
      localStorage.setItem("ecosphere_token", emailOrToken);
      setUser(passwordOrUser);
      return passwordOrUser;
    }
    const data = await authApi.login(emailOrToken, passwordOrUser);
    localStorage.setItem("ecosphere_token", data.access_token);
    setUser(data.user);
    return data.user;
  };

  const setAuthSession = (token, userData) => {
    localStorage.setItem("ecosphere_token", token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("ecosphere_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, setAuthSession, loading, isAdmin: user?.role === "admin", isOfficer: user?.role === "environmental_officer" || user?.role === "admin" }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
