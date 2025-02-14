import {DB} from "$lib/DB";

export async function GET({cookies, params: {code}})
{
    const key = cookies.get("session-key")

    if (key == undefined)
    {
        return new Response("Unauthorized", {status: 401})
    }

    const newDeviceId = await DB.UserConfirmPairing(key, code)

    if (newDeviceId == null)
    {
        return new Response("Invalid code", {status: 400})
    }

    return new Response(newDeviceId)
}
