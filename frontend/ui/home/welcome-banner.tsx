"use client"

import { authRequest } from "@/backend-api/auth";
import LoadingSpinner from "@/components/loader";
import { AUTH_CONSTANTS } from "@/lib/constants";
import { clsx } from "@/lib/utils";
import { redirect } from "next/navigation";
import React from "react";


export default function WelcomeBanner() {
    const [username, setUsername] = React.useState<string>("");
    const [isLoading, setIsLoading] = React.useState(true);
    const [tokenStatus, setTokenStatus] = React.useState("");

    async function checkTokenStatus() {
        const res = await authRequest("/auth/whoami", {method: 'GET'}, false);

        if (!res.ok) {
            const text = await res.text();

            if (text.toLowerCase().includes("revoke")) {
                setTokenStatus("Revoked");
            } else if (text.toLowerCase().includes("unauth")) {
                setTokenStatus("Unauth");
            } else if (text.toLowerCase().includes("expired")) {
                setTokenStatus("Expired");
            } else {
                setTokenStatus("Invalid");
            }

        } else {
            setTokenStatus("Valid");
        }
    }


    async function revokeToken() {
        await authRequest("/auth/revoke", {method: 'POST'}, false);
    }

    React.useEffect(() => {
        async function foo() {
            const res = await authRequest("/auth/whoami", { method: 'GET' });
            setUsername(await res.text());
        }

        foo();
        
        setIsLoading(false);
    });

    return (

        (isLoading ? <LoadingSpinner /> : (
            <div className="flex flex-col items-center justify-center">
                <h1>Welcome to your homepage, {username}</h1>
                <div className="flex flex-row">
                    <button onClick={() => {
                        localStorage.setItem(AUTH_CONSTANTS.tokenName, "");
                        // redirect("/");
                    }} className="border border-black p-2 rounded-md bg-blue-700 text-gray-900 font-bold text-xl m-2 hover:cursor-pointer">
                        Logout
                    </button>
                    <button onClick={async () => {
                        await revokeToken();
                    }} className="border border-black p-2 rounded-md bg-orange-500 text-gray-900 font-bold text-xl m-2 hover:cursor-pointer">
                        Revoke Token
                    </button>
                </div>

                <div className="flex flex-row">
                    <button onClick={async () => {
                        await checkTokenStatus();
                    }} className="border border-white p-2 rounded-md bg-white text-gray-700 font-bold text-xl m-2 hover:cursor-pointer">
                        Current Token Status
                    </button>
                    {tokenStatus &&  <StatusButton status={tokenStatus}/>}
                </div>

            </div>))
    )
}


function StatusButton({status}: {status: string}) {
    React.useEffect(() => {

    }, [status]);

    return (
        <div className={clsx(`border border-black items-center flex p-2 px-3 m-2 rounded-md font-extrabold text-white`, { 'bg-red-600': status !== "Valid", "bg-green-600": status === "Valid" })}>
            {status}
        </div>
    )
}