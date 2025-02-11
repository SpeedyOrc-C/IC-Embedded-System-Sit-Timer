import {DB} from "$lib/DB";

export async function load({cookies})
{
    const sessionKey = cookies.get("session-key")

    if (!sessionKey)
    {
        throw new Error("Not logged in")
    }

    const userId = await DB.GetUserId(sessionKey)

    if (userId == null)
    {
        throw new Error("Not logged in")
    }

    const devices = await DB.GetDevices(userId)

    return {userId, devices}
}
