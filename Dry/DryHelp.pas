unit DryHelp;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Math;

function CreateHelp(ExeName: string; const ProgramDescription: string;
  const Usage: array of string; const Options: array of string): string;

implementation

function RepeatString(const Count: Integer; const Text: string): string;
var
  I: Integer;
begin
  Result := '';
  for I := 1 to Count do
    Result := Result + Text;
end;

function CreateHelp(ExeName: string; const ProgramDescription: string;
  const Usage: array of string; const Options: array of string): string;
var
  UsageLine: string;
  MaxOptionLength: Integer = 0;
  OptionsCount, I, J: Integer;
  OptionLength: array of Integer;
begin
  Assert(not Odd(Length(Options)));
  ExeName := ExtractFileName(ExeName);
  if ProgramDescription = '' then
    Result := ''
  else
    Result := ProgramDescription + LineEnding + LineEnding;
  Result := Result + 'Usage:' + LineEnding;
  for UsageLine in Usage do
    Result := Result + '  ' + ExeName + ' ' + UsageLine + LineEnding;
  Result := Result + LineEnding + 'Options:' + LineEnding;

  OptionsCount := Round(Length(Options) / 2);
  SetLength(OptionLength, OptionsCount);
  for I := 0 to OptionsCount - 1 do
  begin
    J := I * 2;
    OptionLength[I] := Length(Options[J]);
    MaxOptionLength := Max(MaxOptionLength, OptionLength[I]);
  end;
  for I := 0 to OptionsCount - 1 do
  begin
    J := I * 2;
    Result := Result +
      '  ' + Options[J] + RepeatString(MaxOptionLength - OptionLength[I], ' ') +
      '  ' + Options[J + 1];
    if I < OptionsCount - 1 then
      Result := Result + LineEnding;
  end;
end;

end.

