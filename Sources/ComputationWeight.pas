unit ComputationWeight;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils;

type
  ECustom = class(Exception);
  EIrrelevantResult = class(ECustom);

function ComputeWeight(const RackWidth, GateHeight: Extended): Extended;

implementation

const
  HandleWeight = 1.0;

procedure CheckIsPositive(const Value: Extended; const Name: string);
var
  Text: string;
begin
  Text := Format('%s: "%f"', [Name, Value]) + LineEnding;
  if Value < 0 then
    raise EIrrelevantResult.Create(Text + 'Значение отрицательно.');
  if Value = 0 then
    raise EIrrelevantResult.Create(Text + 'Значение равно нулю.');
end;

function ComputeBottomChannelWeight(const BottomChannelLength: Extended
  ): Extended;
begin
  Result := 0.007 * BottomChannelLength + 0.9;
  CheckIsPositive(Result, 'Масса нижней опоры');
end;

function ComputeSideChannelWeight(const SideChannelLength: Extended): Extended;
begin
  Result := 0.007 * SideChannelLength - 0.5;
  CheckIsPositive(Result, 'Масса боковой стойки');
end;

function ComputeRodWeight(const RodLength: Extended): Extended;
begin
  Result := 0.001 * RodLength + 0.72;
  CheckIsPositive(Result, 'Масса круглой стяжки');
end;

function ComputeWallWeight(const WallWidth, WallHeight: Extended): Extended;
begin
  Result := 2.382e-5 * WallWidth * WallHeight + 4.386e-4 * WallWidth +
    0.00568 * WallHeight;
  CheckIsPositive(Result, 'Масса полотна щита');
end;

function ComputeHorizontalStiffenerWeight(
  const HorizontalStiffenerLength: Extended): Extended;
begin
  Result := 0.002 * HorizontalStiffenerLength - 0.544;
  CheckIsPositive(Result, 'Масса горизонтального ребра');
end;

function ComputeVerticalStiffenerWeight(
  const VerticalStiffenerLength: Extended): Extended;
begin
  Result := 0.002 * VerticalStiffenerLength + 0.25;
  CheckIsPositive(Result, 'Масса вертикального ребра');
end;

function ComputeHorizontalStiffenerQty(const GateHeight: Extended): Integer;
const
  Step = 400;
begin
  Result := Trunc(GateHeight / Step);
end;

function ComputeVerticalStiffenerQty(const GateWidth: Extended): Integer;
const
  Step = 400;
begin
  Result := Trunc(GateWidth / Step);
end;

function ComputeRackWeight(const RackWidth, RackHeight: Extended): Extended;
begin
  Result := ComputeBottomChannelWeight(RackWidth) +
    ComputeSideChannelWeight(RackHeight) * 2 +
    ComputeRodWeight(RackWidth - 20) * 2;
end;

function ComputeGateWeight(const GateWidth, GateHeight: Extended): Extended;
var
  HorizontalStiffenerQty, VerticalStiffenerQty: Integer;
begin
  HorizontalStiffenerQty := ComputeHorizontalStiffenerQty(GateHeight);
  VerticalStiffenerQty := ComputeVerticalStiffenerQty(GateWidth);
  Result := ComputeWallWeight(GateWidth, GateHeight) + HandleWeight;
  if HorizontalStiffenerQty > 0 then
    Result := Result +
      ComputeHorizontalStiffenerWeight(GateWidth - 8) * HorizontalStiffenerQty;
  if VerticalStiffenerQty > 0 then
    Result := Result +
      ComputeVerticalStiffenerWeight(GateHeight) * VerticalStiffenerQty;
end;

function ComputeWeightCorrection(const RackWidth, GateHeight: Extended
  ): Extended;
begin
  Result := -5.94e-6 * RackWidth * GateHeight + 0.00722 * RackWidth +
    0.0068 * GateHeight;
  if Result < 0 then
    Result := 0;
end;

function ComputeWeight(const RackWidth, GateHeight: Extended): Extended;
begin
  Result := ComputeRackWeight(RackWidth, GateHeight) +
    ComputeGateWeight(RackWidth - 20, GateHeight) +
    ComputeWeightCorrection(RackWidth, GateHeight);
end;

end.
