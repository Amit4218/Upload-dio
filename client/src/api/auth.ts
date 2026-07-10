import axiosApiClient from "@/api/apiClient";

export const login = async (email: string, password: string) => {
  const res = await axiosApiClient.postForm("/api/auth/login", {
    username: email,
    password,
  });

  localStorage.setItem("authtoken", res.data.access_token);
};
