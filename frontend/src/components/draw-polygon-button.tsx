import { Check, Pencil, X } from "lucide-react"
import { Button } from "./ui/button"

interface DrawPolygonButtonProps {
    isDrawing: boolean
    isReadyToClear: boolean
    clickHandler: () => void
}

export default function DrawPolygonButton({ isDrawing, isReadyToClear, clickHandler }: DrawPolygonButtonProps) {
    return (
        <Button
            onClick={clickHandler}
            size="icon-lg"
            className={`absolute bottom-6 right-6 size-14 rounded-full shadow-lg transition-all
            ${isDrawing ? "bg-emerald-500 hover:bg-emerald-600" :
                    isReadyToClear ? "bg-red-500 hover:bg-red-600" :
                        "bg-white hover:bg-primary/90"}
            `}
        >
            {isDrawing ? (
                <Check className="size-6" color="white" />
            ) : isReadyToClear ? (
                <X className="size-6" color="white" />
            ) : (
                <Pencil className="size-6" />
            )}

            <span className="sr-only">
                {isDrawing ? "Finish drawing" :
                    isReadyToClear ? "Clear drawing" :
                        "Start drawing"}
            </span>
        </Button>
    );
}
