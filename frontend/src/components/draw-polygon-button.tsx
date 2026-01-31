import { Check, Pencil } from "lucide-react"
import { Button } from "./ui/button"

interface DrawPolygonButtonProps {
    isDrawing: boolean
    clickHandler: () => void
}

export default function DrawPolygonButton({ isDrawing, clickHandler }: DrawPolygonButtonProps) {
    return (
        <Button
            onClick={clickHandler}
            size="icon-lg"
            className={`absolute bottom-6 right-6 size-14 rounded-full shadow-lg transition-al ${isDrawing
                ? "bg-emerald-500 hover:bg-emerald-600"
                : "bg-white hover:bg-primary/90"
                }`}
        >
            {isDrawing ? (
                <Check className="size-6" color="white" />
            ) : (
                <Pencil className="size-6" />
            )}
            <span className="sr-only">
                {isDrawing ? "Finish drawing" : "Start drawing"}
            </span>
        </Button>
    )
}