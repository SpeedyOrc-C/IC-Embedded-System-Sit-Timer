import {DB} from "$lib/DB";

export async function GET({cookies})
{
    const key = cookies.get("session-key")

    if (!key)
    {
        return new Response("Not logged in", {status: 401})
    }

    await DB.LogOut(key)

    cookies.delete("session-key", {path: "/", secure: process.env.NODE_ENV != "development"})

    return new Response("BYE")
}
