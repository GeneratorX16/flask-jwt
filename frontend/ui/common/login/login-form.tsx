"use client";

import React from "react";
import {User, KeyRound} from"lucide-react";
import { Plus_Jakarta_Sans } from 'next/font/google'
import CustomInput from "@/components/input";
import { m } from "@/lib/utils";
import { CustomEnv } from "@/env";
import LoadingSpinner from "@/components/loader";

const inter = Plus_Jakarta_Sans({ subsets: ['latin'] })


export default function LoginForm() {
    const [formData, setformData] = React.useState({username: "", password: ""});
    const [isLoading, setIsLoading] = React.useState(false);
    const [formError, setFormError] = React.useState(false);
    
    async function handleSubmit(e: React.MouseEvent<HTMLFormElement, MouseEvent>) {
        e.preventDefault();

        setIsLoading(true);
        const res = await fetch(CustomEnv.BACKEND_BASE_URL + "/auth/login", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!res.ok) {
            setFormError(true);
        } else {
            setFormError(false);
            console.log("Login successfull")
        }
        
    }

    return (
        <div className={m("bg-white text-black flex flex-col justify-center items-center relative p-12", inter.className)}>
            <form onSubmit={(e) => handleSubmit(e)} className="flex flex-col justify-center items-center gap-5 w-full max-w-sm">
                <h1 className="text-2xl font-extrabold">Account Login</h1>
                <div className="flex flex-row bg-gray-100 text-gray-600 border-b border-b-gray-300 focus-within:border-b-black transition duration-500 ease-in-out py-0.5 px-0.5 w-full max-w-sm">
                    <User className="text-gray-500 mr-1 ml-1"/>
                    <CustomInput type="text" value={formData.username} placeholder="Username"
                     onChange={(e) => setformData({...formData, username: e.currentTarget.value})} className="border-none" required/>
                </div>
                <div className="flex flex-row bg-gray-100 text-gray-600 border-b border-b-gray-300 focus-within:border-b-black transition duration-500 ease-in-out py-0.5 px-0.5 w-full max-w-sm">
                    <KeyRound className="text-gray-500 mr-1 ml-1"/>
                    <CustomInput type="password" value={formData.password} placeholder="Password"
                    onChange={(e) => setformData({...formData, password: e.currentTarget.value})} className="border-none" required/>
                </div>
                <button type="submit" className="bg-black text-white px-1 py-1 w-full font-bold hover:cursor-pointer">Login</button>
            </form>
            {formError && <span className="text-red-500 absolute bottom-4 left-0 right-0 text-center">{"username or password incorrect"}</span>}
            <LoadingSpinner />
        </div>
    )
}