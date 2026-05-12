"use client";

import { useState, useCallback } from "react";
import { ToastMessage } from "@/types";

let toastIdCounter = 0;

export function useToast() {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = useCallback(
    (toast: Omit<ToastMessage, "id">) => {
      const id = `toast-${++toastIdCounter}`;
      const newToast: ToastMessage = {
        id,
        duration: 5000,
        ...toast,
      };

      setToasts((prev) => [...prev, newToast]);

      if (newToast.duration && newToast.duration > 0) {
        setTimeout(() => {
          removeToast(id);
        }, newToast.duration);
      }

      return id;
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = {
    success: (title: string, description?: string) =>
      addToast({ title, description, variant: "success" }),
    error: (title: string, description?: string) =>
      addToast({ title, description, variant: "destructive" }),
    warning: (title: string, description?: string) =>
      addToast({ title, description, variant: "warning" }),
    info: (title: string, description?: string) =>
      addToast({ title, description, variant: "default" }),
    custom: (message: Omit<ToastMessage, "id">) => addToast(message),
  };

  return {
    toasts,
    toast,
    removeToast,
  };
}