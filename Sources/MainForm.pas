unit MainForm;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls, Graphics, Dialogs, StdCtrls,
  ExtCtrls, ComputationWeight, DryConversion;

type

  { TForm1 }

  TForm1 = class(TForm)
    ButtonRun: TButton;
    LabeledEditWidth: TLabeledEdit;
    LabeledEditHeight: TLabeledEdit;
    LabeledEditWeight: TLabeledEdit;
    procedure ButtonRunClick(Sender: TObject);
  private

  public

  end;

var
  Form1: TForm1;

implementation

procedure ShowErrorAndSetFocus(const LabeledEdit: TLabeledEdit;
  const Name, Warning: string);
var
  Text: string;
begin
  Text := Name + ': "' + LabeledEdit.Text + '"' + LineEnding + Warning + '.';
  MessageDLG(Text, mtError, [mbOK], 0);
  LabeledEdit.SelectAll;
  LabeledEdit.SetFocus;
end;

{$R *.lfm}

{ TForm1 }

procedure TForm1.ButtonRunClick(Sender: TObject);
const
  RackWidthName = 'Ширина рамы';
  GateHeightName = 'Высота щита';
  IncorrectFloatWarning = 'Ожидается число';
  MinRackWidth = 300.0;
  MaxRackWidth = 3000.0;
  MinGateHeight = 300.0;
  MaxGateHeight = 4000.0;
var
  RackWidth, GateHeight, Weight: Extended;
begin
  LabeledEditWeight.Clear;

  if ConvertStrToFloat(LabeledEditWidth.Text, RackWidth) <> CorrectLine then
  begin
    ShowErrorAndSetFocus(LabeledEditWidth, RackWidthName,
      IncorrectFloatWarning);
    Exit;
  end;
  if RackWidth <= MinRackWidth then
  begin
    ShowErrorAndSetFocus(LabeledEditWidth, RackWidthName,
      Format('Ожидается число больше %.0f', [MinRackWidth]));
    Exit;
  end;
  if RackWidth > MaxRackWidth then
  begin
    ShowErrorAndSetFocus(LabeledEditWidth, RackWidthName,
      Format('Ожидается число не больше %.0f', [MaxRackWidth]));
    Exit;
  end;

  if ConvertStrToFloat(LabeledEditHeight.Text, GateHeight) <> CorrectLine then
  begin
    ShowErrorAndSetFocus(LabeledEditHeight, GateHeightName,
      IncorrectFloatWarning);
    Exit;
  end;
  if GateHeight < MinGateHeight then
  begin
    ShowErrorAndSetFocus(LabeledEditHeight, GateHeightName,
      Format('Ожидается число не меньше %.0f', [MinGateHeight]));
    Exit;
  end;
  if GateHeight > MaxGateHeight then
  begin
    ShowErrorAndSetFocus(LabeledEditHeight, GateHeightName,
      Format('Ожидается число не больше %.0f', [MaxGateHeight]));
    Exit;
  end;

  try
    Weight := ComputeWeight(RackWidth, GateHeight);
  except
    on E: ECustom do
    begin
      MessageDLG(E.Message, mtError, [mbOK], 0);
      Exit;
    end;
  end;
  LabeledEditWeight.Text := Format('%f', [Weight]);
end;

end.

