import {sql} from "@vercel/postgres"

import hash from "hash.js"

function RandomHexString(length: number)
{
    return [...crypto.getRandomValues(new Uint8Array(length >> 1))]
        .map(n => n.toString(16).padStart(2, '0'))
        .join('')
}

export class DB
{
    public static async DoesDeviceExist(id: string)
    {
        const {rows} = await sql`select
                                 from device
                                 where device_id = ${id}`

        return rows.length > 0
    }

    public static async SignUp(username: string, password: string)
    {
        const salt = RandomHexString(8)

        const hashed = hash.sha512().update(password + salt).digest("hex")

        return await sql`insert into "user"
                         values (${username}, ${salt}, ${hashed});`
    }

    public static async LogIn(username: string, password: string)
    {
        const {rows} = await sql`select salt, hash
                                 from "user"
                                 where user_id = ${username};`

        if (rows.length === 0)
        {
            throw new Error("Incorrect username or password")
        }

        const {salt, hash: correctHash} = rows[0]

        const requestHash = hash.sha512().update(password + salt).digest("hex")

        if (requestHash !== correctHash)
        {
            throw new Error("Incorrect username or password")
        }

        const key = RandomHexString(64)

        await sql`insert into session
                  values (${key}, ${username});`

        return key
    }

    public static async LogOut(key: string)
    {
        await sql`delete
                  from session
                  where key = ${key}`
    }

    public static async LogOutFromAllPlaces(key: string)
    {
        await sql`delete
                  from session
                  where user_id = (select user_id
                                   from session
                                   where key = ${key})`
    }

    public static async GetUserId(key: string)
    {
        const {rows} = await sql`select user_id
                                 from session
                                 where key = ${key}`

        if (rows.length == 0)
        {
            return null
        }

        return rows[0].user_id as string
    }

    public static async GetDevices(userId: string)
    {
        const {rows} = await sql`select device_id, name
                                 from device
                                 where owner = ${userId}`

        return rows as { device_id: string, name: string }[]
    }

    public static async GetDeviceName(key: string, id: string)
    {
        const {rows} = await sql`select name
                                 from session
                                          natural join "user"
                                          natural join device
                                 where key = ${key}
                                   and device_id = ${id}`

        if (rows.length == 0)
        {
            return null
        }

        return rows[0].name as string
    }

    public static async SetDeviceName(key: string, id: string, name: string)
    {
        const {rows} = await sql`select user_id
                                 from session
                                          natural join "user"
                                          natural join device
                                 where key = ${key}
                                   and device_id = ${id}`

        if (rows.length == 0)
        {
            return false
        }

        await sql`update device
                  set name = ${name}
                  where device_id = ${id}`

        return true
    }

    public static async DeleteDevice(key: string, id: string)
    {
        const {rows} = await sql`select user_id
                                 from session
                                          natural join "user"
                                          natural join device
                                 where key = ${key}
                                   and device_id = ${id}`

        if (rows.length == 0)
        {
            return false
        }

        await sql`delete
                  from device
                  where device_id = ${id}`

        return true
    }

    public static async DeviceRequestPairing()
    {
        const id = RandomHexString(64)
        const code = RandomHexString(4)

        try
        {
            await sql`delete
                      from pairing
                      where expire_time < now()::timestamp`

            await sql`insert into pairing (new_device_id, code)
                      values (${id}, ${code})`
        }
        catch (e)
        {
            return null
        }

        return {id, code}
    }

    public static async UserConfirmPairing(key: string, code: string)
    {
        const user = await DB.GetUserId(key)

        if (user === null)
        {
            return null
        }

        await sql`delete
                  from pairing
                  where expire_time < now()::timestamp`

        const {rows} = await sql`select new_device_id
                                 from pairing
                                 where code = ${code}`

        if (rows.length == 0)
        {
            return null
        }

        const newDeviceId = rows[0].new_device_id as string

        try
        {
            await sql`delete
                      from pairing
                      where new_device_id = ${newDeviceId}`

            await sql`insert into device (device_id, owner)
                      values (${newDeviceId}, ${user})`
        }
        catch (e)
        {
            return null
        }

        return newDeviceId
    }

    public static async LogYes(id: string)
    {
        try
        {
            await sql`insert into log (device_id, existence)
                      values (${id}, true)`
        }
        catch (e)
        {
            return false
        }

        return true
    }

    public static async LogNo(id: string)
    {
        try
        {
            await sql`insert into log (device_id, existence)
                      values (${id}, false)`
        }
        catch (e)
        {
            return false
        }

        return true
    }

    public static async GetLogs(key: string, id: string)
    {
        try
        {
            const {rows} = await sql`select time, existence
                                     from session
                                              natural join "user"
                                              natural join device
                                              natural join log
                                     where key = ${key}
                                       and device_id = ${id}
                                     order by time asc`

            return rows as { time: string, existence: boolean }[]
        }
        catch (e)
        {
            return null
        }
    }
}
