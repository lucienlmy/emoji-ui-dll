using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowDataGridViewDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new DataGridViewDemoApp().Run();
        }
    }

    internal sealed class DataGridViewDemoApp : DemoApp
    {
        private IntPtr _grid;
        private EmojiWindowNative.DataGridCellCallback _cellClickCallback;
        private EmojiWindowNative.DataGridColumnHeaderCallback _headerClickCallback;
        private int _sortDirection;

        public DataGridViewDemoApp()
            : base("EmojiWindow DataGridView Demo - C# .NET 4.0", 1040, 620)
        {
            _sortDirection = EmojiWindowNative.DataGridSortAsc;
        }

        protected override void Build()
        {
            CreateHeader("DataGridView Demo", "DataGridView sample with sort and callbacks.");

            IntPtr stage = CreateGroupBox(WindowHandle, "DataGridView Stage", 18, 84, 1000, 440, ColorPrimary);
            _grid = EmojiWindowNative.CreateDataGridView(WindowHandle, 46, 153, 940, 320, false, true, ColorText, ColorWhite);
            BuildColumns();
            SeedRows();

            _cellClickCallback = new EmojiWindowNative.DataGridCellCallback(OnCellClick);
            _headerClickCallback = new EmojiWindowNative.DataGridColumnHeaderCallback(OnHeaderClick);
            EmojiWindowNative.DataGrid_SetCellClickCallback(_grid, _cellClickCallback);
            EmojiWindowNative.DataGrid_SetColumnHeaderClickCallback(_grid, _headerClickCallback);

            AddButton(stage, "+", "Add Row", 18, 378, 110, 34, ColorPrimary, AddRow);
            AddButton(stage, "-", "Delete Row", 142, 378, 120, 34, ColorSuccess, RemoveSelectedRow);
            AddButton(stage, "R", "Read Cell", 276, 378, 126, 34, ColorWarning, ReadSelectedCell);
            AddButton(stage, "S", "Sort Col0", 416, 378, 150, 34, ColorDanger, SortByFirstColumn);
        }

        private void BuildColumns()
        {
            byte[] name = U("Task");
            byte[] status = U("Status");
            byte[] owner = U("Owner");
            EmojiWindowNative.DataGrid_AddTextColumn(_grid, name, name.Length, 240);
            EmojiWindowNative.DataGrid_AddTextColumn(_grid, status, status.Length, 160);
            EmojiWindowNative.DataGrid_AddTextColumn(_grid, owner, owner.Length, 160);
            EmojiWindowNative.DataGrid_SetShowGridLines(_grid, 1);
            EmojiWindowNative.DataGrid_SetDefaultRowHeight(_grid, 34);
            EmojiWindowNative.DataGrid_SetHeaderHeight(_grid, 38);
            EmojiWindowNative.DataGrid_SetFreezeHeader(_grid, 1);
            EmojiWindowNative.DataGrid_SetSelectionMode(_grid, EmojiWindowNative.DataGridSelectionCell);
        }

        private void SeedRows()
        {
            AddGridRow("Design", "Doing", "Alice");
            AddGridRow("API", "Pending", "Bob");
            AddGridRow("Test", "Done", "Carol");
        }

        private void AddGridRow(string task, string status, string owner)
        {
            int row = EmojiWindowNative.DataGrid_AddRow(_grid);
            WriteCell(row, 0, task);
            WriteCell(row, 1, status);
            WriteCell(row, 2, owner);
        }

        private void WriteCell(int row, int col, string text)
        {
            byte[] bytes = U(text);
            EmojiWindowNative.DataGrid_SetCellText(_grid, row, col, bytes, bytes.Length);
        }

        private void AddRow()
        {
            AddGridRow("Task " + (EmojiWindowNative.DataGrid_GetRowCount(_grid) + 1), "Pending", "Demo");
            SetStatus("Added one row.");
        }

        private void RemoveSelectedRow()
        {
            int row = EmojiWindowNative.DataGrid_GetSelectedRow(_grid);
            if (row >= 0)
            {
                EmojiWindowNative.DataGrid_RemoveRow(_grid, row);
                SetStatus("Removed row " + row + ".");
            }
            else
            {
                SetStatus("No selected row.");
            }
        }

        private void ReadSelectedCell()
        {
            int row = EmojiWindowNative.DataGrid_GetSelectedRow(_grid);
            int col = EmojiWindowNative.DataGrid_GetSelectedCol(_grid);
            if (row >= 0 && col >= 0)
            {
                SetStatus("Cell text: " + EmojiWindowNative.ReadCellText(_grid, row, col, EmojiWindowNative.DataGrid_GetCellText));
            }
            else
            {
                SetStatus("No selected cell.");
            }
        }

        private void SortByFirstColumn()
        {
            EmojiWindowNative.DataGrid_SortByColumn(_grid, 0, _sortDirection);
            _sortDirection = _sortDirection == EmojiWindowNative.DataGridSortAsc ? EmojiWindowNative.DataGridSortDesc : EmojiWindowNative.DataGridSortAsc;
            SetStatus("Sorted by column 0.");
        }

        private void OnCellClick(IntPtr hGrid, int row, int col)
        {
            SetStatus("Cell callback: row=" + row + ", col=" + col);
        }

        private void OnHeaderClick(IntPtr hGrid, int col)
        {
            SetStatus("Header callback: col=" + col);
        }
    }
}
