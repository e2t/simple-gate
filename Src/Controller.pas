unit Controller;

{$MODE OBJFPC}
{$LONGSTRINGS ON}
{$ASSERTIONS ON}
{$RANGECHECKS ON}
{$BOOLEVAL OFF}

interface

procedure Run();
procedure MainFormInit();

implementation

uses
  ProgramInfo, GuiMainForm, GuiHelper, Measurements, Classes, SysUtils, GateCalculation;

procedure MainFormInit();
begin
  MainForm.Caption := GetProgramTitle;
end;

function CreateInputData(out InputData: TInputData): string;
const
  SIncorrectValue = ' - неправильное значение.';
var
  Value: Double;
begin
  InputData := Default(TInputData);
  Result := '';

  if MainForm.EditFrameWidth.GetRealMinEqMaxEq(Value, ToMm(MinWidth),
    ToMm(MaxWidth)) then
    InputData.FrameWidth := Mm(Value)
  else
    Exit('Ширина рамы' + SIncorrectValue);

  if MainForm.EditGateHeight.GetRealMinEqMaxEq(Value, ToMm(MinHeight),
    ToMm(MaxHeight)) then
    InputData.GateHeight := Mm(Value)
  else
    Exit('Высота щита' + SIncorrectValue);
end;

function CreateOutput(const Slg: TSimpleGate): string;
var
  Lines: TStringList;
begin
  Lines := TStringList.Create;
  Lines.Add(Format('Шандор %sх%s',
    [FormatFloat('0.0##', Slg.FrameWidth), FormatFloat('0.0##', Slg.GateHeight)]));
  Lines.Add('');
  Lines.Add(Format('Масса %.0f кг', [Slg.Weight]));
  Lines.Add(Format('* рамы %.0f кг', [Slg.FrameWeight]));
  Lines.Add(Format('* щита %.0f кг', [Slg.GateWeight]));
  Result := Lines.Text;
  Lines.Free;
end;

procedure PrintOutput(const Text: string);
begin
  MainForm.MemoOutput.Clear;
  MainForm.MemoOutput.Text := Text;
  MainForm.MemoOutput.SelStart := 0;
end;

procedure Run();
var
  InputData: TInputData;
  InputDataError: string;
  Slg: TSimpleGate;
begin
  InputDataError := CreateInputData(InputData);
  if InputDataError = '' then
  begin
    CalcSimpleGate(Slg, InputData);
    PrintOutput(CreateOutput(Slg));
  end
  else
    PrintOutput(InputDataError);
end;

end.
