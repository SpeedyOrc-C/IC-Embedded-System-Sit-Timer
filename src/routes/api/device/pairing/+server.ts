import {DB} from "$lib/DB";

export async function GET()
{
    const res = await DB.DeviceRequestPairing()

    if (res == null)
    {
        return new Response("Generated code is repeated, please try again", {status: 503})
    }

    return new Response(JSON.stringify(res))
}
