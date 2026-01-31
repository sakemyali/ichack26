import { Cartesian2, Cartographic, Ion, ScreenSpaceEventType } from "cesium";
import { useRef, useState } from "react";
import { ScreenSpaceEvent, ScreenSpaceEventHandler, type CesiumComponentRef } from "resium";
import { Viewer as ResiumViewer, } from "resium"
import { Viewer as CesiumViewer } from "cesium";
import { Math as CesiumMath } from "cesium";


Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ACCESS_TOKEN;

type RectangleCoords = Cartographic[]

export default function App() {
  const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);
  const [isDrawingRectangle, setIsDrawingRectangle] = useState<boolean>(false);
  const [drawnRectangleVertices, setDrawnRectangleVertices] = useState<RectangleCoords>([]);

  const handleStartDrawClick = () => {
    console.log("Clicked 'draw rectangle' button.")
    setIsDrawingRectangle(!isDrawingRectangle)
    setDrawnRectangleVertices([])
    if (drawnRectangleVertices.length > 0) {
      console.log(`Completed vertex: ${JSON.stringify(drawnRectangleVertices)}`)
    }
  }

  const handleAddRectangleVertex = (point: Cartographic) => {
    console.log(`Added vertex at ${point}`)
    setDrawnRectangleVertices(prev =>
      [...prev, point] as unknown as RectangleCoords
    );
  };

  const handleMapLeftClick = (e: { position: Cartesian2 }) => {
    if (!isDrawingRectangle) return;

    if (!viewerRef.current?.cesiumElement) return;

    const scene = viewerRef.current?.cesiumElement.scene;
    const camera = viewerRef.current?.cesiumElement.camera;

    const ray = camera.getPickRay(e.position);

    if (!ray) return;

    const cartesian = scene.globe.pick(ray, scene);

    if (!cartesian) return;

    const carto = Cartographic.fromCartesian(cartesian);
    carto.longitude = CesiumMath.toDegrees(carto.longitude);
    carto.latitude = CesiumMath.toDegrees(carto.latitude);

    handleAddRectangleVertex(carto);
  };

  return (
    <main className="flex flex-row h-screen">
      <div className="flex flex-col items-center align-middle">
        <h1 className="my-10">Sidebar</h1>
        <button className="my-10 hover:cursor-pointer" onClick={handleStartDrawClick}>
          Draw rectangle
        </button>
        <p className="text-center">{`Drawing? ${isDrawingRectangle}`}</p>
      </div>
      <ResiumViewer
        className="w-full h-full"
        ref={viewerRef}
        animation={false}
        infoBox={false}
        homeButton={false}
        sceneModePicker={false}
        projectionPicker={false}
        baseLayerPicker={false}
        navigationHelpButton={false}
        timeline={false}
        fullscreenButton={false}
        vrButton={false}
      >
        <ScreenSpaceEventHandler>
          <ScreenSpaceEvent type={ScreenSpaceEventType.LEFT_DOWN} action={(e) => handleMapLeftClick((e as { position: Cartesian2 }))} />
        </ScreenSpaceEventHandler>
      </ResiumViewer>
    </main>
  );
}
