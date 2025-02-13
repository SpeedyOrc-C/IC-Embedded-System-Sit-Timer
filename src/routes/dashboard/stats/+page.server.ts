import {DB, IntervalsFromLogs} from "$lib/DB";

export async function load({cookies})
{
    const key = cookies.get("session-key")

    if (!key)
    {
        throw new Error("Not logged in")
    }

    const maybeDevicesLogs = await DB.GetLogsUnderThisAccount(key)

    if (maybeDevicesLogs === null)
    {
        throw new Error("Logs not found")
    }

    const devices = new Set(maybeDevicesLogs.map(({device_id}) => device_id))

    const devicesLogs =
        new Map(
            new Array(...devices)
                .map(device =>
                    [device,
                        IntervalsFromLogs(maybeDevicesLogs
                            .filter(({device_id: d}) =>
                                device == d
                            )
                            .map(({time, existence}) =>
                                ({time: new Date(time), existence})
                            )
                        )
                    ]
                )
        )

    return {devicesLogs}
}
