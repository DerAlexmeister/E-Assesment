module Problem exposing (..)

import Dict exposing (Dict)
import Four exposing (Four, Index, Karnaugh)
import Set exposing (Set)


type alias MapColoring =
    { karnaugh : Karnaugh
    , coloring : Set (Set ( Index, Index ))
    }


type alias MapConversion =
    { coloring : MapColoring
    }


type alias Minimization =
    { function : Function
    , formula : Int
    }
