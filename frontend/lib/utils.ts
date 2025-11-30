export function m(...args: string[]) {
    return args.map(a => a.trim()).join(" ");
}

export function clsx(...args: ({[key: string]: boolean} | string)[]) {
    let finalClass = "";
    for (const arg of args) {
        if (typeof(arg) === "string") {
            finalClass += arg.trim();
        } else {
            finalClass += Object.keys(arg).filter(k => arg[k]).map(k => k.trim()).join(" ");
        }
    }
}