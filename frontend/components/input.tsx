import { m } from "@/lib/utils";



export default function CustomInput({ className, type, ...props }: React.ComponentProps<"input">) {
    return (
        <input 
        type="text" 
        className={m("border-b outline-none border-b-gray-300 px-1.5 py-0.5 bg-gray-100 text-gray-700 focus:border-b-black transition duration-500 ease-in-out", className ?? "")} 
        {...props}
         />
    )
}