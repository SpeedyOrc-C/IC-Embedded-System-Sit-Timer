import {DB} from "$lib/DB";

export async function POST({request, cookies})
{
    const {username, password} = await request.json()

    try
    {
        const key = await DB.LogIn(username, password)

        cookies.set("session-key", key, {
            path: "/", secure: process.env.NODE_ENV != "development", maxAge: 60 * 60 * 24 * 7
        })
    }
    catch (e)
    {
        return new Response("Incorrect username or password", {status: 401})
    }

    return new Response("Win")
}
