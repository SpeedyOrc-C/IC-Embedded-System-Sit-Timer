import {DB} from "$lib/DB";

export async function load({cookies})
{
    const sessionKey = cookies.get("session-key")

    if (!sessionKey)
    {
        return {userId: null}
    }

    const userId = await DB.GetUserId(sessionKey)

    if (userId == null)
    {
        return {userId}
    }

    const devices = await DB.GetDevices(userId)

    return {userId, devices}
}
