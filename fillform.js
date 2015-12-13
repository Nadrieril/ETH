function selectDropdown(id, n) { $('#contentContainer #'+id+'>option:eq('+n+')').attr('selected', true); }
function fillField(id, v) { $('#contentContainer #'+id).val(v); }
fields = [ 'title', 'academicYear', 'courseNumber', 'weeks', 'hoursTutorial', 'hoursLectures', 'hoursPracticalWork', 'hoursResearch', 'grade', 'credits', 'content', 'literature' ]

function fillForm(obj) {
  selectDropdown('subjectCategory', 1)
  selectDropdown('universityStudiesId', obj.universityStudiesId)
  for(i in fields) {
    var k = fields[i]
    fillField(k, obj[k])
  }
}
fillForm(obj)
$('#store').click()
