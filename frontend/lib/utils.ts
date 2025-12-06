export function m(...args: string[]) {
    return args.map(a => a.trim()).join(" ");
}

export function clsx(...args: ({[key: string]: boolean} | string)[]) {
    const finalClass: string[] = [];
    for (const arg of args) {
        if (typeof(arg) === "string") {
            finalClass.push(arg.trim());
        } else {
            finalClass.push(Object.keys(arg).filter(k => arg[k]).map(k => k.trim()).join(" "))
        }
    }
    return finalClass.join(" ");
}