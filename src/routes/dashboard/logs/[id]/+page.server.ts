import {DB} from "$lib/DB";

export async function load({cookies, params: {id}})
{
    const key = cookies.get("session-key")

    if (!key)
    {
        return null
    }

    const name = await DB.GetDeviceName(key, id)

    const logs = await DB.GetLogs(key, id)

    return {name, logs}
}
