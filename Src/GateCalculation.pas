unit GateCalculation;

{$MODE OBJFPC}
{$LONGSTRINGS ON}
{$ASSERTIONS ON}
{$RANGECHECKS ON}
{$BOOLEVAL OFF}

interface

type
  TInputData = record
    FrameWidth: Double;
    GateHeight: Double;
  end;

  TSimpleGate = record
    FrameWidth: Double;
    GateHeight: Double;
    Weight: Double;
    FrameWeight: Double;
    GateWeight: Double;
  end;

const
  MinWidth = 0.3;
  MaxWidth = 3.0;
  MinHeight = 0.3;
  MaxHeight = 8.0;

procedure CalcSimpleGate(out Slg: TSimpleGate; const InputData: TInputData);

implementation

uses
  Math;

// Швеллер
function CalcMass01ad001(const GateHeight: Double): Double;
begin
  Result := 3.5879 * GateHeight - 0.0079;
  Assert(Result > 0);
end;

// Опора нижняя
function CalcMass01ad002(const FrameWidth: Double): Double;
begin
  Result := 5.6686 * FrameWidth - 0.0057;
  Assert(Result > 0);
end;

// Перемычка
function CalcMass01ad003(const FrameWidth: Double): Double;
begin
  Result := 2.992 * FrameWidth - 0.06;
  Assert(Result > 0);
end;

// Количество скоб на раме
function CalcCount01ad005(const GateHeight: Double): Integer;
const
  Step = 0.4;
begin
  Result := Floor(GateHeight / Step);
  Assert(Result > 0);
end;

// Полотно
function CalcMass02ad001(const FrameWidth, GateHeight: Double): Double;
begin
  Result := 32 * FrameWidth * GateHeight - 0.9602 * GateHeight - 0.009;
  Assert(Result > 0);
end;

// Ребро вертикальное
function CalcMass02ad002(const GateHeight: Double): Double;
begin
  Result := 2.9933 * GateHeight - 0.2301;
  Assert(Result > 0);
end;

// Ребро горизонтальное
function CalcMass02ad003(const FrameWidth: Double): Double;
begin
  Result := 2.992 * FrameWidth - 0.64;
  Assert(Result > 0);
end;

// Количество горизонтальных ребер
function CalcCount02ad003(const GateHeight: Double): Integer;
const
  Step = 0.75;
begin
  Result := 2 + Floor(GateHeight / Step);
  Assert(Result > 0);
end;

function CalcFrameMass(const FrameWidth, GateHeight: Double): Double;
const
  Mass01ad004 = 0.25;  // Проушина
  Mass01ad005 = 0.05;  // Скоба
begin
  Result := CalcMass01ad001(GateHeight) * 4 + CalcMass01ad002(FrameWidth) +
    CalcMass01ad003(FrameWidth) + Mass01ad004 * 2 + Mass01ad005 *
    CalcCount01ad005(GateHeight);
end;

function CalcGateMass(const FrameWidth, GateHeight: Double): Double;
const
  Mass02ad004 = 0.42;  // Проушина на щите
  FastenersMass02ad = 0.12;  // Крепеж щита
begin
  Result := CalcMass02ad001(FrameWidth, GateHeight) + CalcMass02ad002(GateHeight) *
    2 + CalcMass02ad003(FrameWidth) * CalcCount02ad003(GateHeight) +
    Mass02ad004 + FastenersMass02ad;
end;

procedure CalcSimpleGate(out Slg: TSimpleGate; const InputData: TInputData);
begin
  Slg.FrameWidth := InputData.FrameWidth;
  Slg.GateHeight := InputData.GateHeight;

  Slg.FrameWeight := CalcFrameMass(Slg.FrameWidth, Slg.GateHeight);
  Slg.GateWeight := CalcGateMass(Slg.FrameWidth, Slg.GateHeight);
  Slg.Weight := Slg.FrameWeight + Slg.GateWeight;
end;

end.
