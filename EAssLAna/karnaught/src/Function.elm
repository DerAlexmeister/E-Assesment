module Function exposing (..)

import EverySet exposing (EverySet, fromList, toList)
import Four exposing (Four)
import Json.Decode as D
import Json.Encode as E


type alias Function =
    { function : EverySet (Four Bool)
    , variables : Four String
    , function_name : String
    }


encode : Function -> E.Value
encode function =
    E.object
        [ ( "function", toList function.function |> E.list (Four.encode E.bool) )
        , ( "variables", Four.encode E.string function.variables )
        , ( "name", E.string function.function_name )
        ]


functionDecoder : D.Decoder (EverySet (Four Bool))
functionDecoder =
    Four.decoder D.bool
        |> D.list
        |> D.map fromList


decoder : D.Decoder Function
decoder =
    D.map3 Function
        (D.field "function" functionDecoder)
        (D.field "variables" <| Four.decoder D.string)
        (D.field "name" D.string)
