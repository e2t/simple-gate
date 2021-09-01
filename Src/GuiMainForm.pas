unit GuiMainForm;

{$MODE OBJFPC}
{$LONGSTRINGS ON}
{$ASSERTIONS ON}
{$RANGECHECKS ON}
{$BOOLEVAL OFF}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls;

type

  { TMainForm }

  TMainForm = class(TForm)
    ButtonRun: TButton;
    EditGateHeight: TEdit;
    EditFrameWidth: TEdit;
    Label1: TLabel;
    Label2: TLabel;
    MemoOutput: TMemo;
    procedure ButtonRunClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: char);
  private

  public

  end;

var
  MainForm: TMainForm;

implementation

uses
  Controller, LCLType;

{$R *.lfm}

{ TMainForm }

procedure TMainForm.FormKeyPress(Sender: TObject; var Key: char);
begin
  if Key = Chr(VK_RETURN) then
    Run();
end;

procedure TMainForm.ButtonRunClick(Sender: TObject);
begin
  Run();
end;

procedure TMainForm.FormCreate(Sender: TObject);
begin
  MainFormInit();
end;

end.

