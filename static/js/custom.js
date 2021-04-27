function checkaccident()
{
     var insdiv = document.getElementById('insurance');
     var accident = document.getElementById('caraccident').value;
     if(accident == 'Yes')
     {
        insdiv.style.display = "block";
        document.getElementById("insurance_no").required= true;
        document.getElementById("insurance_image").required= true;
     }
     else
     {
        insdiv.style.display = "none";
        document.getElementById("insurance_no").removeAttribute("required");
        document.getElementById("insurance_image").removeAttribute("required");
        document.getElementById("sure").innerHTML = "Are You Sure ?"
     }

}

