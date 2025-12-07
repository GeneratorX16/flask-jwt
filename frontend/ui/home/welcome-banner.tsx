"use client"

import { authRequest } from "@/backend-api/auth";
import { AUTH_CONSTANTS } from "@/lib/constants";
import { redirect } from "next/navigation";
import React from "react";


export default function WelcomeBanner() {
    const [username, setUsername] = React.useState<string>("");
    const [isLoading, setIsLoading] = React.useState(true);

    React.useEffect(() => {
        async function foo() {
            const res = await authRequest("/auth/whoami", {method: 'GET'});
            setUsername(await res.text());
        }

        foo();
         setIsLoading(false);
    }, []);

    return (

        (isLoading ? null : (
        <div className="flex flex-col items-center justify-center">
            <h1>Welcome to your homepage, {username}</h1>
            <button onClick={() => {
                localStorage.setItem(AUTH_CONSTANTS.tokenName, "");
                redirect("/");
            }} className="border border-white p-2 rounded-md bg-white text-gray-700 font-bold text-xl m-2 hover:cursor-pointer">
                Logout
            </button>
        </div>))
    )
}