"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuthStore } from "@/store/auth-store";
import { authApi } from "@/lib/apis";
import { toast } from "sonner";

export function useAuth() {
  const router = useRouter();
  const { setUser, setToken, logout: storeLogout } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await authApi.login(email, password);
      const { user, access_token } = res.data;
      setUser(user);
      setToken(access_token);
      toast.success("Welcome back!", {
        description: `Logged in as ${user.name}`,
      });
      router.push("/prompt-studio");
    } catch (err: unknown) {
      const message =
        (err as { response?: { data?: { detail?: string } } })?.response
          ?.data?.detail ?? "Login failed";
      toast.error("Authentication failed", { description: message });
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (
    name: string,
    email: string,
    password: string
  ) => {
    setIsLoading(true);
    try {
      const res = await authApi.register(name, email, password);
      const { user, access_token } = res.data;
      setUser(user);
      setToken(access_token);
      toast.success("Account created!", {
        description: "Welcome to PromptIO",
      });
      router.push("/prompt-studio");
    } catch (err: unknown) {
      const message =
        (err as { response?: { data?: { detail?: string } } })?.response
          ?.data?.detail ?? "Registration failed";
      toast.error("Registration failed", { description: message });
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } finally {
      storeLogout();
      router.push("/auth/login");
      toast.success("Logged out successfully");
    }
  };

  return { login, register, logout, isLoading };
}