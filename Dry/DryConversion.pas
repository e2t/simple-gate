unit DryConversion;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils;

type
  TInputLineCode = (CorrectLine, IncorrectLine, EmptyLine);

const
  GravAcceleration = 9.80665;  { m/s2 }

function ConvertStrToInt(const Text: string;
  out Number: Integer): TInputLineCode;
function ConvertStrToFloat(const Text: string;
  out Number: Extended): TInputLineCode;

function ToMPa(const Pa: Extended): Extended;
function FromKg(const Kg: Extended): Extended;
function ToMm(const Meters: Extended): Extended;

implementation

function ConvertStrToInt(const Text: string;
  out Number: Integer): TInputLineCode;
begin
  if Text = '' then
    Result := EmptyLine
  else
    try
      Number := StrToInt(Text);
      Result := CorrectLine;
    except
      on EConvertError do
        Result := IncorrectLine;
    end;
end;

function ConvertStrToFloat(const Text: string;
  out Number: Extended): TInputLineCode;
begin
  if Text = '' then
    Result := EmptyLine
  else
    try
      Number := StrToFloat(Text);
      Result := CorrectLine;
    except
      on EConvertError do
        Result := IncorrectLine;
    end;
end;

function ToMPa(const Pa: Extended): Extended;
begin
  Result := Pa / 1e6;
end;

function FromKg(const Kg: Extended): Extended;
begin
  Result := Kg * GravAcceleration;
end;

function ToMm(const Meters: Extended): Extended;
begin
  Result := Meters * 1e3;
end;

end.

