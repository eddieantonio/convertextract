import pympi
from convertextract.parsers.utils import BaseParser

class Parser(BaseParser):
    """Extract text from ELAN file using pympi-ling.
    """

    def extract(self, filename, **kwargs):
        if 'mapping' in kwargs and kwargs['mapping']:
            transducer = self.create_transducer(kwargs['mapping'])
        else:
            transducer = self.get_transducer(kwargs.get('input_language', ''), 
                                             kwargs.get('output_language', ''))
            converted_filename = filename[:-4] + '_converted.eaf'
        print("SUCCESS", converted_filename)
        # Here is where you should parse and convert the Elan file
        eaf_obj = pympi.Elan.Eaf(filename)
        tiers = eaf_obj.get_tier_names() #returned as a list
        all_results = []
        for tier in tiers:
            result = eaf_obj.get_annotation_data_for_tier(tier) #Gives a list of annotations of the form: (begin, end, value)
            #iterates over each list within the tiers
            for res in result:
                #change value in place to a string
                #converts 'value' using g2p
                #adds converted data to all_results
                value_res = str(res[2])
                new_res = transducer(value_res).output_string
                all_results.append(new_res)

                value_res.remove_all_annotations_from_tier(tiers)
                value_res.add_annotation(tiers, value = "new_res")

        if "no_write" in kwargs or kwargs['no_write']:
            pass
        else:
            pympi.Elan.to_eaf(converted_filename, eaf_obj, pretty=True)
        return ' '.join(all_results)


#if __name__ == '__main__':
#    print('helloooo')
    # put your stuff here

#convertextract path/to/foo.eaf -il eng-ipa -ol eng-arpabet