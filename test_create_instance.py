def test_create_instance(isLess, isUseRegionForUntin, isUseRegionForSur):
    if isLess == ' ':
        isLess = ''
    if isUseRegionForUntin == ' ':
        isUseRegionForUntin = ''
    if isUseRegionForSur == ' ':
        isUseRegionForSur = ''


    if isLess == '1' and isUseRegionForUntin == '1' and isUseRegionForSur == '1':
        print('less, regionUntin, regionSur')

    if isLess == '1' and isUseRegionForUntin == '1' and isUseRegionForSur == '':
        print('less, regionUntin, distanceSur')

    if isLess == '1' and isUseRegionForUntin == '' and isUseRegionForSur == '1':
        print('less, distanceUntin, regionSur')

    if isLess == '1' and isUseRegionForUntin == '' and isUseRegionForSur == '':
        print('less, distanceUntin, distanceSur')

    if isLess == '' and isUseRegionForUntin == '1' and isUseRegionForSur == '1':
        print('Lessthan, regionUntin, regionSur')

    if isLess == '' and isUseRegionForUntin == '1' and isUseRegionForSur == '':
        print('lessthan, regionUntin, distanceSur')

    if isLess == '' and isUseRegionForUntin == '' and isUseRegionForSur == '1':
        print('lessthan, distanceUntin, regionSur')
        
    if isLess == '' and isUseRegionForUntin == '' and isUseRegionForSur == '':
        print('lessthan, distanceUntin, distanceSur')



isLess = ' '
isUseRegionForUntin = ' '
isUseRegionForSur = ''
test_create_instance(isLess, isUseRegionForUntin, isUseRegionForSur)
