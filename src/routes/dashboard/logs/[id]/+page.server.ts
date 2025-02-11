import {DB} from "$lib/DB";

export async function load({cookies, params: {id}})
{
    const key = cookies.get("session-key")

    if (!key)
    {
        throw new Error("Not logged in")
    }

    const name = await DB.GetDeviceName(key, id)

    if (name === null)
    {
        throw new Error("Device not found")
    }

    const logs = await DB.GetLogs(key, id)

    if (logs === null)
    {
        throw new Error("Logs not found")
    }

    return {name, logs}
}
