var TableRow = {
    selected:-1,
    hoverColor:'#CCCCCC',
    defaultColor:'#EEEEFF',
    onmouseover : function(trow,id)
    {
        if (TableRow.selected!= id)
            trow.bgColor=TableRow.hoverColor;
    },
    onmouseout : function(trow,id)
    {
        if (TableRow.selected!= id)
            trow.bgColor=TableRow.defaultColor;
    },
    onclick : function(trow,id)
    {
        if (TableRow.selected == id)
        {
            TableRow.selected = -1;
            trow.bgColor=TableRow.hoverColor;
        }
        else
        {
            var r = document.getElementById('id_tablerow_'+TableRow.selected);
            if (TableRow.selected !=-1 && r)
               r.bgColor=TableRow.defaultColor;
            TableRow.selected = id;
            trow.bgColor=TableRow.hoverColor;
        }
    }
}