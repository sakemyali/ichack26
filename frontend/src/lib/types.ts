import type { Cartographic } from "cesium"

export type PolygonCoords = Cartographic[]
export interface OSMAddress {
    country?: string
    ocean?: string
    sea?: string
}
export interface DrawingState {
    isDrawing: boolean
    isClearable: boolean
    isCompleted: boolean
}