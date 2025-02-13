export function PadZero(n: number)
{
    return n < 10 ? `0${n}` : n
}

export function ReadableDuration(ms: number)
{
    const s = ms / 1000

    if (s < 60)
    {
        return `Less than 1 min`
    }

    const m = s / 60

    if (m < 60)
    {
        return `${Math.floor(m)} min`
    }

    const h = m / 60

    if (m % 60 < 1)
    {
        return `${Math.floor(h)} hour`
    }

    return `${Math.floor(h)} hour ${Math.floor(m % 60)} min`
}

export function ReadableShortDuration(ms: number)
{
    const s = ms / 1000

    if (s < 60)
    {
        return `< 1 m`
    }

    const m = s / 60

    if (m < 60)
    {
        return `${Math.floor(m)} m`
    }

    const h = m / 60

    if (m % 60 < 1)
    {
        return `${Math.floor(h)} h`
    }

    return `${Math.floor(h)} h ${Math.floor(m % 60)} m`
}
