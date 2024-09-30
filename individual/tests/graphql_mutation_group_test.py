import json
from individual.tests.test_helpers import (
    create_group,
    create_individual,
    create_group_with_individual,
    IndividualGQLTestCase,
    complete_group_tasks,
)


class GroupGQLMutationTest(IndividualGQLTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_group_general_permission(self):
        query_str = f'''
            mutation {{
              createGroup(
                input: {{
                  code: "GF"
                  individualsData: []
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # Anonymous User has no permission
        response = self.query(query_str)

        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # IMIS admin can do everything
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

        # Health Enrollment Officier (role=1) has no permission
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.med_enroll_officer_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

    def test_create_group_row_security(self):
        query_str = f'''
            mutation {{
              createGroup(
                input: {{
                  code: "GBVA"
                  individualsData: []
                  villageId: {self.village_a.id}
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # SP officer B cannot create group for district A
        response = self.query(query_str)
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer A can create group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B can create group for district B
        response = self.query(
            query_str.replace(
                f'villageId: {self.village_a.id}',
                f'villageId: {self.village_b.id}'
            ), headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B can create group without any district
        response = self.query(
            query_str.replace(f'villageId: {self.village_a.id}', ' '),
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

    def test_update_group_general_permission(self):
        group = create_group(self.admin_user.username)
        query_str = f'''
            mutation {{
              updateGroup(
                input: {{
                  id: "{group.id}"
                  code: "GFOO"
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # Anonymous User has no permission
        response = self.query(query_str)

        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # IMIS admin can do everything
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_success(id)

        # Health Enrollment Officier (role=1) has no permission
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.med_enroll_officer_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

    def test_update_group_row_security(self):
        group_a = create_group(
            self.admin_user.username,
            payload_override={'village': self.village_a},
        )
        query_str = f'''
            mutation {{
              updateGroup(
                input: {{
                  id: "{group_a.id}"
                  code: "GBAR"
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # SP officer B cannot update group for district A
        response = self.query(query_str)
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer A can update group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B can update group without any district
        group_no_loc = create_group(self.admin_user.username)
        response = self.query(
            query_str.replace(
                f'id: "{group_a.id}"',
                f'id: "{group_no_loc.id}"'
            ), headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_success(id)

    def test_delete_group_general_permission(self):
        group1 = create_group(self.admin_user.username)
        group2 = create_group(self.admin_user.username)
        query_str = f'''
            mutation {{
              deleteGroup(
                input: {{
                  ids: ["{group1.id}", "{group2.id}"]
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # Anonymous User has no permission
        response = self.query(query_str)

        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # Health Enrollment Officier (role=1) has no permission
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.med_enroll_officer_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # IMIS admin can do everything
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_success(id)

    def test_delete_group_row_security(self):
        group_a1 = create_group(
            self.admin_user.username,
            payload_override={'village': self.village_a},
        )
        group_a2 = create_group(
            self.admin_user.username,
            payload_override={'village': self.village_a},
        )
        group_b = create_group(
            self.admin_user.username,
            payload_override={'village': self.village_b},
        )
        query_str = f'''
            mutation {{
              deleteGroup(
                input: {{
                  ids: ["{group_a1.id}"]
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # SP officer B cannot delete group for district A
        response = self.query(query_str)
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer A can delete group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B can delete group without any district
        group_no_loc = create_group(self.admin_user.username)
        response = self.query(
            query_str.replace(
                str(group_a1.id),
                str(group_no_loc.id)
            ), headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B cannot delete a mix of groups from district A and district B
        response = self.query(
            query_str.replace(
                f'["{group_a1.id}"]',
                f'["{group_a1.id}", "{group_b.id}"]'
            ), headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer B can delete group from district B
        group_no_loc = create_group(self.admin_user.username)
        response = self.query(
            query_str.replace(
                str(group_a1.id),
                str(group_b.id)
            ), headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['deleteGroup']['internalId']
        self.assert_mutation_success(id)

    def test_add_individual_to_group_general_permission(self):
        group = create_group(self.admin_user.username)
        individual = create_individual(self.admin_user.username)
        query_str = f'''
            mutation {{
              addIndividualToGroup(
                input: {{
                  groupId: "{group.id}"
                  individualId: "{individual.id}"
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # Anonymous User has no permission
        response = self.query(query_str)

        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # Health Enrollment Officier (role=1) has no permission
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.med_enroll_officer_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # IMIS admin can do everything
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_success(id)

    def test_add_individual_to_group_row_security(self):
        group_a = create_group(
            self.admin_user.username,
            payload_override={'village': self.village_a},
        )
        group_b = create_group(
            self.admin_user.username,
            payload_override={'village': self.village_b},
        )
        group_no_loc = create_group(self.admin_user.username)

        individual_a = create_individual(
            self.admin_user.username,
            payload_override={'village': self.village_a},
        )
        individual_b = create_individual(
            self.admin_user.username,
            payload_override={'village': self.village_b},
        )
        individual_no_loc = create_individual(self.admin_user.username)

        query_str = f'''
            mutation {{
              addIndividualToGroup(
                input: {{
                  groupId: "{group_a.id}"
                  individualId: "{individual_a.id}"
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # SP officer B cannot add individual to group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer B can add individual to group for district B
        query_str_b = query_str.replace(
            str(individual_a.id), str(individual_b.id)
        ).replace(
            str(group_a.id), str(group_b.id)
        )
        response = self.query(
            query_str_b,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer A can add individual to group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer A can add individual without location to group in district A
        response = self.query(
            query_str.replace(str(individual_a.id), str(individual_no_loc.id)),
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer A can add individual from district A to group without location
        response = self.query(
            query_str.replace(str(group_a.id), str(group_no_loc.id)),
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_success(id)

        # Adding a individual to a group with different locations is not allowed
        response = self.query(
            query_str.replace(str(group_a.id), str(group_b.id)),
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['addIndividualToGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.individual_group_village_mismatch')

    def test_edit_individual_in_group_general_permission(self):
        individual, group, group_individual = create_group_with_individual(self.admin_user.username)
        query_str = f'''
            mutation {{
              editIndividualInGroup(
                input: {{
                  id: "{group_individual.id}"
                  groupId: "{group.id}"
                  individualId: "{individual.id}"
                  role: HEAD
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # Anonymous User has no permission
        response = self.query(query_str)

        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # Health Enrollment Officier (role=1) has no permission
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.med_enroll_officer_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # IMIS admin can do everything
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_success(id)

    def test_edit_individual_in_group_row_security(self):
        individual, group, group_individual = create_group_with_individual(self.admin_user.username)
        individual_a, group_a, group_individual_a = create_group_with_individual(
            self.admin_user.username,
            group_override={'village': self.village_a},
            individual_override={'village': self.village_a},
        )
        individual_b, group_b, group_individual_b = create_group_with_individual(
            self.admin_user.username,
            group_override={'village': self.village_b},
            individual_override={'village': self.village_b},
        )
        query_str = f'''
            mutation {{
              editIndividualInGroup(
                input: {{
                  id: "{group_individual_a.id}"
                  groupId: "{group_a.id}"
                  individualId: "{individual_a.id}"
                  role: HEAD
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # SP officer B cannot update individual in group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer B can edit individual in group for district B
        query_str_b = query_str.replace(
            str(individual_a.id), str(individual_b.id)
        ).replace(
            str(group_a.id), str(group_b.id)
        ).replace(
            str(group_individual_a.id), str(group_individual_b.id)
        )
        response = self.query(
            query_str_b,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_success(id)

        complete_group_tasks(group_a.id)
        complete_group_tasks(group_b.id)

        # SP officer A can edit individual in group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_success(id)

        complete_group_tasks(group_a.id)

        # SP officer A can move individual without location to group in district A
        query_str_no_loc = query_str.replace(
            str(individual_a.id), str(individual.id)
        ).replace(
            str(group_individual_a.id), str(group_individual.id)
        )
        response = self.query(
            query_str_no_loc,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_success(id)

        complete_group_tasks(group.id)

        # SP officer A can move individual from district A to group without location
        response = self.query(
            query_str.replace(str(group_a.id), str(group.id)),
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_success(id)

        # Moving a individual to a group with different locations is not allowed
        response = self.query(
            query_str.replace(str(group_a.id), str(group_b.id)),
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['editIndividualInGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.individual_group_village_mismatch')
