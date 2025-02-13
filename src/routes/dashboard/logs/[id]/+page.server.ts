import {DB, IntervalsFromLogs} from "$lib/DB";

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

    const maybeLogs: { time: string; existence: boolean }[] | null = await DB.GetLogsOfDevice(key, id)

    if (maybeLogs === null)
    {
        throw new Error("Logs not found")
    }

    const logs = maybeLogs.map(({time, existence}) => ({time: new Date(time), existence}))

    const intervals = IntervalsFromLogs(logs)

    return {name, logs, intervals}
}
