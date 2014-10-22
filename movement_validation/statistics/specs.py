# -*- coding: utf-8 -*-
"""
This is the Python port of 
https://github.com/JimHokanson/SegwormMatlabClasses/blob/master/%2Bseg_worm/%2Bstats/specs.m
and its subclasses,
https://github.com/JimHokanson/SegwormMatlabClasses/blob/master/%2Bseg_worm/%2Bstats/movement_specs.m
and
https://github.com/JimHokanson/SegwormMatlabClasses/blob/master/%2Bseg_worm/%2Bstats/simple_specs.m
and
https://github.com/JimHokanson/SegwormMatlabClasses/blob/master/%2Bseg_worm/%2Bstats/event_specs.m

In other words, this module defines the classes
- Specs
- MovementSpecs
- SimpleSpecs
- EventSpecs,
the latter three of which are subclasses of the first.

"""
import os
import csv


class Specs(object):
    """
    
    Notes
    ------------------
    Formerly seg_worm.stats.specs
    
    """
    def __init__(self):
       self.feature_field = None
       self.feature_category = None
       self.resolution = None
       self.is_zero_bin = None
       self.is_signed = None
       self.name = None
       self.short_name = None
       self.units = None


    @property
    def long_field(self):
        """
        Formerly getLongField

        """
        return self.feature_field

    
    @staticmethod
    def getObjectsHelper(csv_path, class_function_handle):
        """


        Parameters
        ----------------------
        csv_path:
        class_function_handle:


        Notes
        ---------------------
        Formerly function objs = seg_worm.stats.specs.getObjectsHelper(csv_path,class_function_handle,prop_names,prop_types)
        
        The inherited objects can give relatively simple
        instructions on how their properties should be interpreted
        from their CSV specification file.

        TODO: 
        It would be nice to do the reading and object construction in 
        here but Matlab is awkward for dynamic object creation 
        - @JimHokanson
        """
        stats_instances = []    

        # See below comment above prop_types
        data_types = {1: str, 2: float, 3: int, 4: bool}

        with open(csv_path) as feature_metadata_file:
            feature_metadata = csv.DictReader(feature_metadata_file)
            # The first row of the CSV file contains the field names.
            
            # The second row of the CSV file contains information about 
            # what kind of data is held in each column:
            #    1 = str
            #    2 = float
            #    3 = int
            #    4 = bool
            #   (this mapping was recorded above in data_types)
            field_data_types = next(feature_metadata)
    
            # The third to last rows of the CSV file contain the feature
            # metadata.  Let's now create a stats_instance for each
            # of these rows, initializing them with the row's metadata.
            for row in feature_metadata:
                # Dynamically create an instance of the right kind 
                # of class
                stats_instance = class_function_handle()
                
                for field in row:
                    # Blank values are given the value None
                    value = None
                    if(row[field] != ''):
                        # Here we are dynamically casting the element 
                        # to the correct data type of the field,
                        # which was recorded in the prop_types dictionary.
                        data_type = data_types[int(field_data_types[field])]
                        value = data_type(row[field])
                    # Dynamically assign the field's value to the 
                    # member data element of the same name in the object
                    setattr(stats_instance, field, value)

                # Only append this row to our list if there is 
                # actually a name.  If not it's likely just a blank row.
                if stats_instance.feature_field:
                    stats_instances.append(stats_instance)
            
        return stats_instances    
    


    
class MovementSpecs(Specs):
    """
    %
    %   Class:
    %   seg_worm.stats.movement_specs
    %
    %   This class specifies how to treat each movement related feature for
    %   histogram processing.
    %
    %
    %   Access via static method:
    %   seg_worm.stats.movement_specs.getSpecs()
    %
    %   See Also:
    %   seg_worm.stats.hist.createHistograms
    %
    %   TODO:
    %   - might need to incorporate seg_worm.w.stats.wormStatsInfo
    %   - remove is_time_series entry ...
    """

    def __init__(self):
        self.index = None
        self.is_time_series = None# TODO: This can be removed
        #%feature_category
        #%resolution
        #%is_zero_bin %This might not be important
        #%is_signed   %I think this dictates having 4 or 16 events ...
        #%        name
        #%        short_name
        #%        units

    @staticmethod
    def getSpecs():
        """
        Formerly objs = getSpecs()
        %seg_worm.stats.movement_specs.getSpecs();

        """
        csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'feature_metadata',
                                'movement_features.csv')
        
        # Return a list of MovementSpecs instances, one instance for each
        # row in the csv_path CSV file.  Each row represents a feature. 
        return Specs.getObjectsHelper(csv_path, MovementSpecs)
    

class SimpleSpecs(Specs):
    """
    %
    %   Class:
    %   seg_worm.stats.simple_specs
    %
    """
    def __init__(self):
        pass

    def getData(self, feature_obj):
        pass
        # TODO: translate this line:
        # return eval(['feature_obj.' obj.feature_field]); 

    @staticmethod
    def getSpecs():
        """    
        Formerly function objs = getSpecs()
            %
            %
            %   s_specs = seg_worm.stats.simple_specs.getSpecs();
            %
            %
        """
        csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'feature_metadata',
                                'simple_features.csv')
        
        # Return a list of MovementSpecs instances, one instance for each
        # row in the csv_path CSV file.  Each row represents a feature. 
        return Specs.getObjectsHelper(csv_path, SimpleSpecs)


class EventSpecs(Specs):
    """

    Notes
    --------------------------
    Formerly seg_worm.stats.event_specs

    """
    def __init__(self):
        self.sub_field = None
        # True will indicate that the data should be negated ...
        self.signed_field = '' 
        self.make_zero_if_empty = None
        self.remove_partials = None


    @property
    def long_field(self):
        """
        Give the "long" version of the instance's name.

        Returns
        ----------------------
        A string, which is a .-delimited concatenation of 
        feature_field and sub_field.
        
        Notes
        ----------------------
        Formerly function value = getLongField(obj)
        """
        value = self.feature_field

        if ~isempty(self.sub_field):
            value = value + '.' + self.sub_field

        return value

   
    @staticmethod
    def getSpecs():
        """    
        Formerly function objs = getSpecs()
            %
            %
            %   s_specs = seg_worm.stats.event_specs.getSpecs();
            %
            %
        """
        csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'feature_metadata',
                                'event_features.csv')
      
        # Return a list of MovementSpecs instances, one instance for each
        # row in the csv_path CSV file.  Each row represents a feature. 
        return Specs.getObjectsHelper(csv_path, EventSpecs)

    
    def getData(self, feature_obj, num_samples):
        """
        Formerly  function data = getData(obj,feature_obj,n_samples)
        
        NOTE: Because we are doing structure array indexing, we need to capture
        multiple outputs using [], otherwise we will only get the first value
        ...
        
        """            
        print("NOTE TO MICHAEL: You'll need to translate EventSpecs.getData now!")

        """
        # TODO: Perhaps we'll add a property in the new object instead
        #       of this poor check ...
        is_old_code = isstruct(feature_obj);

        if is_old_code:
            start_value = 0;
            end_value   = n_samples; # BUG IN OLD CODE: n_samples matches
            # behavior, n_samples -1 does not
            
            # Except, for locomotion.motion.forward.frames - yikes!
            if strcmp(obj.feature_field,'locomotion.motion.forward.frames'):
                end_value = end_value - 1;
        else:
            start_value = 1;
            end_value   = n_samples;

        data = sl.struct.getSubField(feature_obj,obj.feature_field);
            
        if ~isempty(data):
            if ~isempty(obj.sub_field):
                # This will go from:
                #    frames (structure array)
                # to:
                #    frames.time
                # for example.
                # 
                # It is also used for event.ratio.time and event.ratio.distance
                #      going from:
                #          ratio (structure or [])
                #      to:
                #          ratio.time
                #          ratio.distance
                parent_data = data;
                
                data = [data.(obj.sub_field)];
                
                if self.is_signed:
                    negate_mask = [parent_data.(obj.signed_field)];
                    data(negate_mask) = -1*data(negate_mask);
                
                if self.remove_partials:
                    starts = [parent_data.start];
                    ends   = [parent_data.end];

                    remove_mask = false(1,length(starts));

                    if starts(1) == start_value:
                        remove_mask(1) = true;

                    if ends(end) == end_value:
                        remove_mask(end) = true;
                    
                    data(remove_mask) = [];
                
            else:
                # Check things that don't currently make sense unless
                # nested in the way that we expect (i.e. in the frames
                # struct)
                pass
                # TODO: Can't be signed
                # TODO: Can't remove partials
        
        if isempty(data) && obj.make_zero_if_empty:
            data = 0;
        """
        pass

