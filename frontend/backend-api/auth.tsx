import { CustomEnv } from "@/env";
import { AUTH_CONSTANTS } from "@/lib/constants";


export async function authRequest(relativePath: string, options: RequestInit) {
    const token = localStorage.getItem(AUTH_CONSTANTS.tokenName);

    const res = await fetch(CustomEnv.BACKEND_BASE_URL + relativePath, {
        ...options,
        headers: {
            ...options.headers,
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    }
    );

    if (!res.ok) {
        throw new Error("Authorization failed");
    }

    return res;
}