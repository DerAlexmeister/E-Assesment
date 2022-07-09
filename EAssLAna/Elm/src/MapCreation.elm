module MapCreation exposing (..)

import Four exposing (Karnaugh)
import Function exposing (Function)
import Json.Decode as D
import Json.Encode as E


type alias Problem =
    { function : Function }


decoder : D.Decoder Problem
decoder =
    D.map Problem Function.decoder


encodeProblem : Problem -> E.Value
encodeProblem problem =
    Function.encode problem.function


type alias Guess =
    { problem : Problem
    , karnaugh : Karnaugh
    }


encode : Guess -> E.Value
encode guess =
    E.object
        [ ( "problem", encodeProblem guess.problem )
        , ( "karnaugh", Four.encode (Four.encode E.bool) guess.karnaugh )
        ]
