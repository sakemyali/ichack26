import type { OSMAddress, PolygonCoords } from "./types";

function getCentroid(coords: PolygonCoords) {
    const lon = coords.reduce((sum, c) => sum + c.longitude, 0) / coords.length;
    const lat = coords.reduce((sum, c) => sum + c.latitude, 0) / coords.length;
    return { lat, lon };
}

function getBestName(address: OSMAddress) {
    return (
        address.country ||
        address.ocean ||
        address.sea ||
        "???"
    );
}

export async function fetchAreaName(coords: PolygonCoords) {
    const { lat, lon } = getCentroid(coords);

    const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&zoom=10&addressdetails=1`;

    const res = await fetch(url, {
        headers: { "User-Agent": "ICHack26/1.0" }
    });

    const data = await res.json();

    console.log(data.address)
    return getBestName(data.address || {});
}