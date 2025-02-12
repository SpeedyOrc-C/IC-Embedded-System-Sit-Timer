import {DB} from "$lib/DB";

function IntervalsFromLogs(_logs: { time: Date; existence: boolean }[]): { start: Date, end: Date }[]
{
    const logs = _logs.slice()

    // Remove first "stand up" record
    if (logs.length > 0 && !logs[0].existence)
    {
        logs.shift()
    }

    // Remove last "stand down" record
    if (logs.length > 0 && logs[logs.length - 1].existence)
    {
        logs.pop()
    }

    const normalizedLogs: { time: Date, existence: boolean }[] = []

    if (logs.length > 0)
    {
        let {existence: lastExistence} = logs[0]

        normalizedLogs.push(logs[0])

        logs.shift()

        for (const log of logs)
        {
            if (log.existence != lastExistence)
            {
                normalizedLogs.push(log)
                lastExistence = log.existence
            }
        }
    }

    const intervals: { start: Date, end: Date }[] = []

    for (let i = 0; i < normalizedLogs.length / 2; i += 1)
    {
        intervals.push({start: normalizedLogs[i * 2].time, end: normalizedLogs[i * 2 + 1].time})
    }

    return intervals
}

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

    const maybeLogs: { time: string; existence: boolean }[] | null = await DB.GetLogs(key, id)

    if (maybeLogs === null)
    {
        throw new Error("Logs not found")
    }

    const logs = maybeLogs.map(({time, existence}) => ({time: new Date(time), existence}))

    const intervals = IntervalsFromLogs(logs)

    return {name, logs, intervals}
}
