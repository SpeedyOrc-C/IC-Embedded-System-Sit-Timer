import {DB, IntervalsFromLogs} from "$lib/DB";

export async function load({cookies})
{
    const key = cookies.get("session-key")

    if (!key)
    {
        throw new Error("Not logged in")
    }

    const userId = await DB.GetUserId(key)

    if (userId == null)
    {
        throw new Error("Not logged in")
    }

    const maybeDevicesLogs = await DB.GetLogsUnderThisAccount(key)

    if (maybeDevicesLogs === null)
    {
        throw new Error("Logs not found")
    }

    const devices = await DB.GetDevices(userId)

    const devicesLogs =
        new Map(
            new Array(...devices.map(({device_id}) => device_id))
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

    return {userId, devices, devicesLogs}
}
